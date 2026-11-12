import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { AxiosError } from "axios";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const getApiErrorMessage = (error: unknown, fallback: string): string => {
  if (!(error instanceof AxiosError)) return fallback;
  if (!error.response) return "No se pudo conectar con el servidor";

  const message = (error.response.data as { message?: unknown } | undefined)?.message;
  if (typeof message === "string" && message) return message;

  if (message && typeof message === "object") {
    const errors = Object.values(message).flat().filter((e) => typeof e === "string");
    if (errors.length > 0) return errors.join(" · ");
  }

  return fallback;
};
