export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={`animate-pulse bg-gray-200 rounded-lg ${className}`} />;
}

export function FormSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm space-y-4">
      <Skeleton className="h-4 w-32" />
      <div className="grid md:grid-cols-3 gap-4">
        <div className="space-y-2"><Skeleton className="h-3 w-16" /><Skeleton className="h-9 w-full" /></div>
        <div className="space-y-2"><Skeleton className="h-3 w-16" /><Skeleton className="h-9 w-full" /></div>
        <div className="space-y-2"><Skeleton className="h-3 w-16" /><Skeleton className="h-9 w-full" /></div>
      </div>
      <Skeleton className="h-9 w-48" />
    </div>
  );
}
