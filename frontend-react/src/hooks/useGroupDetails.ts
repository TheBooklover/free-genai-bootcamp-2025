import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchGroupDetails, type GroupDetails } from '../services/api';

export function useGroupDetails(groupId: number): UseQueryResult<GroupDetails, Error> {
  return useQuery({
    queryKey: ['group', groupId],
    queryFn: () => fetchGroupDetails(groupId),
    staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
  });
} 