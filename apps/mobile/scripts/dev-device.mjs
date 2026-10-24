import { spawn } from "node:child_process";
import { once } from "node:events";
import { createServer, isIPv4 } from "node:net";
import { networkInterfaces } from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { createDeviceProxy } from "./device-proxy.mjs";

const privateIPv4 = (value) => {
  if (!isIPv4(value)) {
    return false;
  }
  const [a, b] = value.split(".").map(Number);
  return (
    a === 10 || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168)
  );
};
const ipNumber = (value) =>
  value.split(".").reduce((result, part) => result * 256 + Number(part), 0);
const portNumber = (value) => {
  const port = Number(value);
  if (!Number.isInteger(port) || port < 1024 || port > 65_535) {
    throw new Error("Ports must be integers between 1024 and 65535.");
  }
  return port;
};
export const deviceOptions = (values, interfaces = networkInterfaces()) => {
  const addresses = Object.values(interfaces)
    .flat()
    .filter((entry) => entry && entry.family === "IPv4" && !entry.internal);
  const hotspot = addresses.find(
    (entry) =>
      entry.address.startsWith("172.20.10.") &&
      entry.netmask === "255.255.255.240"
  );
  const host = values.host ?? hotspot?.address;
  const local = addresses.find((entry) => entry.address === host);
  const peer =
    values.device ?? (host === hotspot?.address ? "172.20.10.1" : undefined);
  if (
    !host ||
    !peer ||
    !local ||
    !privateIPv4(host) ||
    !privateIPv4(peer) ||
    host === peer
  ) {
    throw new Error(
      "Connect this Mac to your iPhone Personal Hotspot, or pass --host <Mac LAN IPv4> --device <phone LAN IPv4> on the same trusted network."
    );
  }
  const subnetSize = 2 ** 32 - ipNumber(local.netmask);
  if (
    Math.floor(ipNumber(host) / subnetSize) !==
    Math.floor(ipNumber(peer) / subnetSize)
  ) {
    throw new Error("The Mac and phone must be on the same local subnet.");
  }
  const metroPort = portNumber(values.port ?? "8081");
  const port = portNumber(values["proxy-port"] ?? "8082");
  if (metroPort === port) {
    throw new Error("Metro and proxy ports must differ.");
  }
  return { host, metroPort, peer, port };
};
const ensureFreePort = async (port) => {
  const probe = createServer();
  try {
    const listening = once(probe, "listening");
    probe.listen(port, "127.0.0.1");
    await listening;
    const closed = once(probe, "close");
    probe.close();
    await closed;
  } catch {
    throw new Error(
      `Metro port ${port} is already in use. Stop the existing Metro terminal first, or use --port <unused-port>.`
    );
  }
};
const main = async () => {
  const { values } = parseArgs({
    options: {
      device: { type: "string" },
      help: { type: "boolean" },
      host: { type: "string" },
      port: { type: "string" },
      "proxy-port": { type: "string" },
    },
  });
  if (values.help) {
    process.stdout.write(
      "Usage: pnpm --filter @tricorder/mobile dev:device [--host <Mac IPv4> --device <phone IPv4>] [--port 8081] [--proxy-port 8082]\nAuto-detects an iPhone Personal Hotspot. For Wi-Fi, supply both addresses. Only the specified phone can connect.\n"
    );
    return;
  }
  const options = deviceOptions(values);
  await ensureFreePort(options.metroPort);
  const proxy = createDeviceProxy(options);
  const sockets = new Set();
  proxy.on("connection", (socket) => {
    sockets.add(socket);
    socket.once("close", () => sockets.delete(socket));
  });
  try {
    const listening = once(proxy, "listening");
    proxy.listen(options.port, options.host);
    await listening;
  } catch (error) {
    throw new Error(
      `Cannot start phone proxy at ${options.host}:${options.port}: ${error.message}. Stop any previous phone-proxy process or choose --proxy-port <unused-port>.`,
      { cause: error }
    );
  }
  const origin = `http://${options.host}:${options.port}`;
  process.stdout.write(
    `Phone-only Metro access: ${origin} (allowed device ${options.peer})\nKeep the hotspot/network connected and scan the QR code in your Tricorder development build.\n`
  );
  const child = spawn(
    process.execPath,
    [
      "--dns-result-order=ipv4first",
      "./node_modules/expo/bin/cli",
      "start",
      "--localhost",
      "--dev-client",
      "--port",
      String(options.metroPort),
    ],
    {
      cwd: fileURLToPath(new URL("../", import.meta.url)),
      env: {
        ...process.env,
        EXPO_PACKAGER_PROXY_URL: origin,
        EXPO_PUBLIC_API_URL: origin,
      },
      stdio: "inherit",
    }
  );
  let stopping = false;
  const stop = () => {
    if (stopping) {
      return;
    }
    stopping = true;
    proxy.close();
    for (const socket of sockets) {
      socket.destroy();
    }
    if (child.exitCode === null) {
      child.kill("SIGTERM");
    }
  };
  process.once("SIGINT", stop);
  process.once("SIGTERM", stop);
  try {
    const [code] = await once(child, "exit");
    process.exitCode = code ?? 0;
  } finally {
    stop();
  }
};

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href
) {
  try {
    await main();
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}
