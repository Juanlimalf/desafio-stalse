import { Spinner } from "flowbite-react";

export default function Loading() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4">
      <Spinner size="xl" />
      <p className="text-lg text-gray-700 dark:text-gray-300">Carregando...</p>
    </div>
  );
}
