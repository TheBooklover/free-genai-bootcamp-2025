import { useGroupDetails } from '../hooks/useGroupDetails';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from './ui/card';
import { Skeleton } from './ui/skeleton';
import { formatDate } from '../lib/utils';
import type { ReactElement } from 'react';

interface GroupDetailsProps {
  groupId: number;
}

export default function GroupDetails({ groupId }: GroupDetailsProps) {
  const { data, isLoading, error } = useGroupDetails(groupId);

  if (error) {
    return (
      <div className="p-4 text-red-500">
        Error loading group details: {error.message}
      </div>
    );
  }

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <div data-testid="skeleton-header">
            <Skeleton className="h-8 w-[200px]" />
          </div>
        </CardHeader>
        <CardContent>
          <div data-testid="skeleton-content">
            <Skeleton className="h-4 w-[150px]" />
            <Skeleton className="h-4 w-[100px]" />
            <Skeleton className="h-4 w-[120px]" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{data.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div>Words: {data.word_count}</div>
        {data.success_rate !== undefined && (
          <div>Success Rate: {(data.success_rate * 100).toFixed(1)}%</div>
        )}
        {data.last_studied_at && (
          <div>Last Studied: {formatDate(data.last_studied_at)}</div>
        )}
        {data.description && <p>{data.description}</p>}
      </CardContent>
    </Card>
  );
} 