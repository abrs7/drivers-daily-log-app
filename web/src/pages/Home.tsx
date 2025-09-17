import { TripForm } from "@/components/TripForm";

export function Home() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Trip Planner</h1>
      <TripForm />
    </div>
  );
}
