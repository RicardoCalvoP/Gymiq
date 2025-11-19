import { createContext, useContext, useState } from "react";

const UserContext = createContext();

export function UserProvider({ children }) {
  const [activeUserId, setActiveUserId] = useState("u1");

  return (
    <UserContext.Provider value={{ activeUserId, setActiveUserId }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}
