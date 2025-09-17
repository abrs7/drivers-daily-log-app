import { api } from "./client";

export interface PlanRequest {
  current_location: string;
  pickup_location: string;
  dropoff_location: string;
  cycle_used_hours: number;
}

export async function planTrip(data: PlanRequest) {
  const res = await api.post("/routing/plan", data);
  return res.data;
}
