import { useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { planTrip } from "@/api/plan";
import { RouteMap } from "@/components/RouteMap";
import { Link } from "react-router-dom";

export function Plan() {
  const { state } = useLocation();
  const { data, isLoading, error } = useQuery({
    queryKey: ["plan", state],
    queryFn: () => planTrip(state),
  });

  if (isLoading) return <div className="p-6">Loading route...</div>;
  if (error) return <div className="p-6 text-red-600">Error planning trip</div>;

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-bold">Planned Route</h2>
      <div className="w-full max-w-3xl">
        <RouteMap geometry={data.route.geometry} />

        <h3 className="text-lg font-semibold mt-6">Daily Segments</h3>
<div className="overflow-x-auto">
  <table className="w-full border-collapse border border-gray-300">
    <thead className="bg-gray-100">
      <tr>
        <th className="border border-gray-300 px-3 py-2">Start</th>
        <th className="border border-gray-300 px-3 py-2">End</th>
        <th className="border border-gray-300 px-3 py-2">Status</th>
        <th className="border border-gray-300 px-3 py-2">Note</th>
      </tr>
    </thead>
    <tbody>
      {data.hos_plan.days[0].segments.map((seg: any, idx: number) => (
        <tr key={idx}>
          <td className="border px-3 py-2">{seg.start}</td>
          <td className="border px-3 py-2">{seg.end}</td>
          <td className="border px-3 py-2 capitalize">{seg.status.replace("_", " ")}</td>
          <td className="border px-3 py-2">{seg.note}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

      </div>
      <Link to="/logs" className="text-blue-600 underline">
  View Daily Logs
</Link>
    </div>
    
  );
}
