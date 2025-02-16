import { useQuery } from '@tanstack/react-query';
import { fetchGroupWords, GroupWordsResponse } from '../services/api';

export interface UseGroupWordsParams {
  groupId: number;
  page: number;
  per_page: number;
  sort_by: string;
  order: 'asc' | 'desc';
}

export function useGroupWords(params: UseGroupWordsParams) {
  return useQuery<GroupWordsResponse>({
    queryKey: ['group-words', params],
    queryFn: () => fetchGroupWords(
      params.groupId,
      params.page,
      params.per_page,
      params.sort_by,
      params.order
    )
  });
} 