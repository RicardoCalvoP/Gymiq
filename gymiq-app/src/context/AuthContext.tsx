import React from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

import { createContext, useContext, useState, useEffect, ReactNode  } from "react";

import * as authApi from "../api/auth";

// Environment variables from react-native-dotenv (@env)
import { AUTH_KEY } from "@env";

type AuthPayload = {
  token: string;
  user: any;
};

type AuthContextType = {
  user: AuthPayload | null;
  isLoaded: boolean;
  signIn: (credentials: { email: string; password: string }) => Promise<void>;
  signUp: (credentials: { email: string; password: string }) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider ({ children }: AuthProviderProps): React.ReactElement {
  const [user, setUser] = useState<AuthPayload | null>(null)
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    const loadUser = async () => {
      try {
        const stored = await AsyncStorage.getItem(AUTH_KEY);
        if (stored) {
          const parsed = JSON.parse(stored);
          setUser(parsed);
        }
      } catch (e) {
        console.log("Error loading saved user: ", e);
      } finally {
        setIsLoaded(true);
      }
    };

    loadUser();
  }, []);

  const signIn = async ({ email, password }: { email: string; password: string }) => {
    try {
      const tokenData = await authApi.login(email, password);
      const me = await authApi.getMe(tokenData.access_token);

      const authPayload: AuthPayload = {
        token: tokenData.access_token,
        user: me,
      };

      setUser(authPayload);
      await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(authPayload));
    } catch (err) {
      // Fallback for local/offline development: create a minimal local user
      console.warn("Auth API failed, falling back to local auth:", err);
      const fallback: AuthPayload = {
        token: "local-token",
        user: { id: email, email },
      };
      setUser(fallback);
      await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(fallback));
    }
  };

  const signUp = async ({ email, password }: { email: string; password: string }) => {
    try {
      const tokenData = await authApi.signup(email, password);
      const me = await authApi.getMe(tokenData.access_token);

      const authPayload: AuthPayload = {
        token: tokenData.access_token,
        user: me,
      };

      setUser(authPayload);
      await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(authPayload));
    } catch (err) {
      // Fallback for local/offline development
      console.warn("Signup API failed, falling back to local signup:", err);
      const fallback: AuthPayload = {
        token: "local-token",
        user: { id: email, email },
      };
      setUser(fallback);
      await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(fallback));
    }
  };


  const signOut = async () => {
    setUser(null);
    await AsyncStorage.removeItem(AUTH_KEY);
  }

  return (
    <AuthContext.Provider value={{user, isLoaded, signIn, signUp, signOut}}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth need to be inside a AuthProvider");
  }
  return ctx;
}
