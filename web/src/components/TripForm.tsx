import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";

export function TripForm() {
  const [form, setForm] = useState({
    current_location: "",
    pickup_location: "",
    dropoff_location: "",
    cycle_used_hours: 0,
  });

  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // pass form state to /plan
    navigate("/plan", { state: form });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto p-6">
      <Input
        name="current_location"
        placeholder="Current location"
        value={form.current_location}
        onChange={handleChange}
      />
      <Input
        name="pickup_location"
        placeholder="Pickup location"
        value={form.pickup_location}
        onChange={handleChange}
      />
      <Input
        name="dropoff_location"
        placeholder="Dropoff location"
        value={form.dropoff_location}
        onChange={handleChange}
      />
      <Input
        name="cycle_used_hours"
        type="number"
        placeholder="Cycle hours used"
        value={form.cycle_used_hours}
        onChange={handleChange}
      />
      <Button
  type="submit"
  className="w-full bg-blue-600 text-gray-900 font-semibold hover:bg-blue-700 hover:text-white"
>
  Plan Trip
</Button>


    </form>
  );
}
