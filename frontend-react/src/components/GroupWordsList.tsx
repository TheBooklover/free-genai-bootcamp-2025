import { useState } from 'react';
import { useGroupWords } from '../hooks/useGroupWords';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Skeleton } from './ui/skeleton';
import { Pagination } from './ui/pagination';
import { Button } from './ui/button';
import { ArrowDownIcon, ArrowUpIcon, ArrowsUpDownIcon } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import { Word } from '../services/api';

interface SortableColumn {
  key: string;
  label: string;
}

const SORTABLE_COLUMNS: SortableColumn[] = [
  { key: 'quebecois', label: 'Term' },
  { key: 'standard_french', label: 'Definition' },
  { key: 'created_at', label: 'Added Date' }
];

interface GroupWordsListProps {
  groupId: number;
}

export default function GroupWordsList({ groupId }: GroupWordsListProps) {
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('quebecois');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  
  const { data, isLoading, error } = useGroupWords({
    groupId,
    page,
    per_page: 10,
    sort_by: sortBy,
    order
  });

  const handleSort = (columnKey: string) => {
    if (sortBy === columnKey) {
      setOrder(order === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(columnKey);
      setOrder('asc');
    }
  };

  const getSortIcon = (columnKey: string) => {
    if (sortBy !== columnKey) {
      return <ArrowsUpDownIcon className="ml-2 h-4 w-4" />;
    }
    return order === 'asc' ? 
      <ArrowUpIcon className="ml-2 h-4 w-4" /> : 
      <ArrowDownIcon className="ml-2 h-4 w-4" />;
  };

  if (error) {
    return (
      <Card>
        <CardContent>
          <div className="text-red-500">
            Error loading words: {error.message}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Words in Group</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              {SORTABLE_COLUMNS.map((column) => (
                <TableHead key={column.key}>
                  <Button
                    variant="ghost"
                    onClick={() => handleSort(column.key)}
                    className="flex items-center font-semibold"
                  >
                    {column.label}
                    {getSortIcon(column.key)}
                  </Button>
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 10 }).map((_, i) => (
                <TableRow key={i}>
                  <TableCell>
                    <Skeleton className="h-4 w-[100px]" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-4 w-[200px]" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-4 w-[100px]" />
                  </TableCell>
                </TableRow>
              ))
            ) : (
              data?.words.map((word: Word) => (
                <TableRow key={word.id}>
                  <TableCell>{word.quebecois}</TableCell>
                  <TableCell>{word.standard_french}</TableCell>
                  <TableCell>{new Date(word.created_at).toLocaleDateString()}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
        {data && (
          <Pagination
            className="mt-4"
            currentPage={page}
            totalPages={data.total_pages}
            onPageChange={setPage}
          />
        )}
      </CardContent>
    </Card>
  );
} 