import { useParams } from 'react-router-dom';
import { useGroupDetails } from '../hooks/useGroupDetails';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from './ui/card';
import { Skeleton } from './ui/skeleton';
import GroupWordsList from './GroupWordsList';
import { ErrorBoundary } from './ErrorBoundary';

export default function GroupDetails() {
  const { groupId } = useParams<{ groupId: string }>();
  const { data: group, isLoading, error } = useGroupDetails(Number(groupId));

  if (error) {
    return (
      <Card>
        <CardContent>
          <div className="text-red-500">
            Error loading group: {error.message}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-[200px]" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-4 w-[300px]" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!group) {
    return null;
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>{group.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div>
              <span className="font-medium">Word Count:</span> {group.word_count}
            </div>
            {group.description && (
              <div>
                <span className="font-medium">Description:</span> {group.description}
              </div>
            )}
            {group.last_studied_at && (
              <div>
                <span className="font-medium">Last Studied:</span>{' '}
                {new Date(group.last_studied_at).toLocaleDateString()}
              </div>
            )}
            {group.success_rate !== undefined && (
              <div>
                <span className="font-medium">Success Rate:</span>{' '}
                {Math.round(group.success_rate * 100)}%
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <ErrorBoundary>
        <GroupWordsList groupId={Number(groupId)} />
      </ErrorBoundary>
    </div>
  );
} 