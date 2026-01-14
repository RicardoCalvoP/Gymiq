// app/context/AuthContext.js
import AsyncStorage from "@react-native-async-storage/async-storage";

import { createContext, useContext, useState, useEffect  } from "react";
import { AUTH_KEY } from "@env";

import * as authApi from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider ({children}) {
  const [user, setUser] = useState(null)
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

  const signIn = async ({ email, password }) => {
    const tokenData = await authApi.login(email, password);
    const me = await authApi.getMe(tokenData.access_token);

    const authPayload = {
      token: tokenData.access_token,
      user: me,
    };

    setUser(authPayload);
    await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(authPayload));
  };

  const signUp = async ({ email, password }) => {
    const tokenData = await authApi.signup(email, password);
    const me = await authApi.getMe(tokenData.access_token);

    const authPayload = {
      token: tokenData.access_token,
      user: me,
    };

    setUser(authPayload);
    await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(authPayload));
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