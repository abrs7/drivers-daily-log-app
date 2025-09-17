import { useEffect, useState } from "react";

export function Logs() {
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const imgs: string[] = [];
        let day = 0;
        while (true) {
          const url = `${import.meta.env.VITE_API_BASE || "http://localhost:8000/api"}/logs/${day}.png`;
          // test if this log exists
          const res = await fetch(url);
          if (!res.ok) break; // stop if not found
          const blob = await res.blob();
          imgs.push(URL.createObjectURL(blob));
          day++;
        }
        setImages(imgs);
      } catch (e) {
        console.error("Error fetching log sheets:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchImages();
  }, []);

  if (loading) return <p className="p-6">Loading log sheets…</p>;

  if (images.length === 0)
    return <p className="p-6 text-red-600">No log sheets found. Run a plan first.</p>;

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold">Daily Log Sheets</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {images.map((src, idx) => (
          <div key={idx} className="border rounded shadow-sm p-2 bg-white">
            <h3 className="text-center font-semibold mb-2">Day {idx + 1}</h3>
            <img src={src} alt={`Log sheet day ${idx + 1}`} className="w-full rounded" />
          </div>
        ))}
      </div>
    </div>
  );
}
