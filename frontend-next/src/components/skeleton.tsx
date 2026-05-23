export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={`animate-pulse bg-gray-200 rounded-lg ${className}`} />;
}

export function KpiSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm space-y-2">
      <Skeleton className="h-3 w-20" />
      <Skeleton className="h-6 w-16" />
      <Skeleton className="h-3 w-24" />
    </div>
  );
}

export function ChartSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm space-y-3">
      <Skeleton className="h-4 w-48" />
      <Skeleton className="h-48 w-full" />
    </div>
  );
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

export function ResultsSkeleton() {
  return (
    <div className="space-y-4 mt-6">
      <Skeleton className="h-10 w-full" />
      <div className="bg-white rounded-xl border border-gray-100 p-5 shadow-sm space-y-3">
        <Skeleton className="h-5 w-64" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-3/4" />
      </div>
      <div className="bg-white rounded-xl border border-gray-100 p-5 shadow-sm space-y-3">
        <Skeleton className="h-5 w-32" />
        <div className="grid grid-cols-3 gap-4">
          <Skeleton className="h-16" />
          <Skeleton className="h-16" />
          <Skeleton className="h-16" />
        </div>
      </div>
    </div>
  );
}
