import React from "react";
import { createContext, useContext, useState, ReactNode } from "react";

type UserContextType = {
  activeUserId: string;
  setActiveUserId: (id: string) => void;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

type UserProviderProps = {
  children: ReactNode;
};

export function UserProvider({ children }: UserProviderProps): React.ReactElement {
  const [activeUserId, setActiveUserId] = useState("u1");

  return (
    <UserContext.Provider value={{ activeUserId, setActiveUserId }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}
