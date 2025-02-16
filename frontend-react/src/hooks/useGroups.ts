import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchGroups, type GroupsResponse } from '../services/api';

export interface UseGroupsParams {
  page: number;
  per_page: number;
  sort_by: string;
  order: 'asc' | 'desc';
}

export function useGroups(params: UseGroupsParams): UseQueryResult<GroupsResponse, Error> {
  return useQuery({
    queryKey: ['groups', params],
    queryFn: () => fetchGroups(
      params.page,
      params.per_page,
      params.sort_by,
      params.order
    ),
    placeholderData: keepPreviousData,
    staleTime: 1000 * 60 // Consider data fresh for 1 minute
  });
} 