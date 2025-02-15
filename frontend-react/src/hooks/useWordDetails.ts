import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchWordDetails, type Word } from '../services/api';

export function useWordDetails(wordId: string | number): UseQueryResult<Word, Error> {
  return useQuery({
    queryKey: ['word', wordId],
    queryFn: () => fetchWordDetails(wordId),
    enabled: !!wordId,
  });
} 