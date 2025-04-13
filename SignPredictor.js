// src/components/SignPredictor.jsx
import { useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";

export default function SignPredictor() {
  const [isPredicting, setIsPredicting] = useState(false);

  const handleStart = async () => {
    try {
      await axios.post("http://localhost:5000/start_prediction");
      setIsPredicting(true);
    } catch (error) {
      console.error("Error starting prediction:", error);
    }
  };

  const handleStop = async () => {
    try {
      await axios.post("http://localhost:5000/stop_prediction");
      setIsPredicting(false);
    } catch (error) {
      console.error("Error stopping prediction:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-gray-800 flex flex-col items-center justify-center p-6 text-white">
      <motion.h1
        className="text-4xl md:text-5xl font-bold mb-10"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        🧠 AI Sign Language Prediction
      </motion.h1>

      <motion.div
        className={`w-80 h-80 rounded-2xl shadow-xl border-4 ${
          isPredicting ? "border-green-400 animate-pulse" : "border-gray-700"
        } flex items-center justify-center text-xl`}
        initial={{ scale: 0.9 }}
        animate={{ scale: isPredicting ? 1.05 : 1 }}
      >
        {isPredicting ? "🟢 Predicting..." : "🔴 Prediction Stopped"}
      </motion.div>

      <div className="flex gap-6 mt-10">
        {!isPredicting ? (
          <button
            onClick={handleStart}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-xl shadow-lg text-lg transition-all duration-200 ease-in-out"
          >
            Start Prediction
          </button>
        ) : (
          <button
            onClick={handleStop}
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-xl shadow-lg text-lg transition-all duration-200 ease-in-out"
          >
            Stop Prediction
          </button>
        )}
      </div>
    </div>
  );
}
