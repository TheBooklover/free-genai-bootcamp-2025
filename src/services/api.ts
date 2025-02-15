import { api } from '@/lib/axios';

// Add or update Word interface
export interface Word {
  id: number;
  quebecois: string;
  standard_french: string;
  english: string;
  pronunciation?: string;
  usage_notes?: string;
  correct_count: number;
  wrong_count: number;
  groups?: Array<{
    id: number;
    name: string;
  }>;
}

// Add fetch function
export const fetchWordDetails = async (wordId: string | number): Promise<Word> => {
  const response = await api.get(`/words/${wordId}`);
  return response.data.word;
}; 