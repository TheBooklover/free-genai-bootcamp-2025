import { useState } from 'react';
import { useGroups } from '../hooks/useGroups';
import { Group } from '../services/api';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import {
  ChevronDownIcon,
  ChevronUpIcon,
  ChevronsUpDownIcon,
} from '@radix-ui/react-icons';
import { formatDate } from '../lib/utils';
import { useNavigation } from '../contexts/NavigationContext';
import { useRouter } from '@tanstack/react-router';

type SortField = 'name' | 'word_count' | 'created_at';

export default function GroupsList() {
  const router = useRouter();
  const { setCurrentGroup } = useNavigation();
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState<SortField>('name');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  const perPage = 10;

  const { data, isLoading, error } = useGroups({
    page,
    per_page: perPage,
    sort_by: sortBy,
    order,
  });

  const handleSort = (field: SortField) => {
    if (sortBy === field) {
      setOrder(order === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setOrder('asc');
    }
  };

  const getSortIcon = (field: SortField) => {
    if (sortBy !== field) return <ChevronsUpDownIcon className="w-4 h-4" />;
    return order === 'asc' ? (
      <ChevronUpIcon className="w-4 h-4" />
    ) : (
      <ChevronDownIcon className="w-4 h-4" />
    );
  };

  const handleGroupClick = (group: Group) => {
    setCurrentGroup(group);
    router.push(`/groups/${group.id}`);
  };

  if (error) {
    return (
      <div className="p-4 text-red-500">
        Error loading groups: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>
              <Button
                variant="ghost"
                onClick={() => handleSort('name')}
                className="flex items-center gap-1"
              >
                Name {getSortIcon('name')}
              </Button>
            </TableHead>
            <TableHead>
              <Button
                variant="ghost"
                onClick={() => handleSort('word_count')}
                className="flex items-center gap-1"
              >
                Words {getSortIcon('word_count')}
              </Button>
            </TableHead>
            <TableHead>
              <Button
                variant="ghost"
                onClick={() => handleSort('created_at')}
                className="flex items-center gap-1"
              >
                Created {getSortIcon('created_at')}
              </Button>
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading ? (
            // Loading skeleton rows
            Array.from({ length: perPage }).map((_, i) => (
              <TableRow key={i} data-testid="skeleton-row">
                <TableCell>
                  <Skeleton className="h-4 w-[200px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[60px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[120px]" />
                </TableCell>
              </TableRow>
            ))
          ) : (
            data?.groups.map((group) => (
              <TableRow 
                key={group.id}
                className="cursor-pointer hover:bg-muted/50"
                onClick={() => handleGroupClick(group)}
              >
                <TableCell>{group.name}</TableCell>
                <TableCell>{group.word_count}</TableCell>
                <TableCell>{formatDate(group.created_at)}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>

      {data && (
        <div className="flex justify-center gap-2">
          <Button
            variant="outline"
            disabled={page === 1}
            onClick={() => setPage(p => p - 1)}
          >
            Previous
          </Button>
          <span className="py-2">
            Page {page} of {data.total_pages}
          </span>
          <Button
            variant="outline"
            disabled={page === data.total_pages}
            onClick={() => setPage(p => p + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
} 