import assert from "node:assert/strict";
import test from "node:test";

import { deviceOptions } from "../scripts/dev-device.mjs";

const interfaces = {
  en0: [
    {
      address: "172.20.10.2",
      family: "IPv4",
      internal: false,
      netmask: "255.255.255.240",
    },
  ],
};
test("phone launcher detects hotspot and keeps Metro on a separate port", () => {
  assert.deepEqual(deviceOptions({}, interfaces), {
    host: "172.20.10.2",
    metroPort: 8081,
    peer: "172.20.10.1",
    port: 8082,
  });
  assert.equal(
    deviceOptions({ port: "8090", "proxy-port": "8091" }, interfaces).port,
    8091
  );
});
test("phone launcher refuses unknown/public/self/off-subnet addresses and invalid ports", () => {
  for (const values of [
    { device: "172.20.10.1", host: "0.0.0.0" },
    { device: "8.8.8.8" },
    { device: "172.20.10.2" },
    { device: "192.168.0.1" },
    { port: "abc" },
    { port: "80" },
    { port: "8082" },
  ]) {
    assert.throws(() => deviceOptions(values, interfaces));
  }
  assert.throws(() => deviceOptions({}, {}));
});
test("Wi-Fi mode requires explicit local host and phone IP", () => {
  const wifi = {
    en0: [
      {
        address: "192.168.1.8",
        family: "IPv4",
        internal: false,
        netmask: "255.255.255.0",
      },
    ],
  };
  assert.throws(() => deviceOptions({}, wifi));
  assert.throws(() => deviceOptions({ host: "192.168.1.8" }, wifi));
  assert.equal(
    deviceOptions({ device: "192.168.1.9", host: "192.168.1.8" }, wifi).peer,
    "192.168.1.9"
  );
});
