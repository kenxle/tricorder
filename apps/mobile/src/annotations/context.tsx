import { createContext, useContext, useMemo } from "react";
import type { PropsWithChildren } from "react";

interface Scope {
  id: string;
  label: string;
}
const Context = createContext<Scope | null>(null);

// Scope IDs identify the company/room and section, never a render position.
export const AnnotationScope = ({
  id,
  label,
  children,
}: PropsWithChildren<Scope>) => {
  const scope = useMemo(() => ({ id, label }), [id, label]);
  return <Context.Provider value={scope}>{children}</Context.Provider>;
};

export const useAnnotationScope = () => useContext(Context);

export const WithoutAnnotations = ({ children }: PropsWithChildren) => (
  <Context.Provider value={null}>{children}</Context.Provider>
);

// Identify repeated labels by their owning evidence/item, not just their words.
export const AnnotationItem = ({
  id,
  label,
  children,
}: PropsWithChildren<Scope>) => {
  const parent = useAnnotationScope();
  return parent ? (
    <AnnotationScope
      id={`${parent.id}/${id}`}
      label={`${parent.label} · ${label}`}
    >
      {children}
    </AnnotationScope>
  ) : (
    children
  );
};
