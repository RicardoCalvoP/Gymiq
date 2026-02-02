// Using @env which is configured by react-native-dotenv
import { AUTH_KEY } from "@env";

import { apiRequest } from "./client";

type LoginResponse = {
  access_token: string;
  [key: string]: any;
};

type UserData = {
  [key: string]: any;
};

export async function login(email: string, password: string): Promise<LoginResponse> {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function signup(email: string, password: string): Promise<LoginResponse> {
  return apiRequest("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getMe(token: string): Promise<UserData> {
  return apiRequest("/users/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
