import { useParams, Link } from 'react-router-dom'
import { useQuery, UseQueryOptions } from '@tanstack/react-query'
import { api } from '@/lib/axios'
import { useNavigation } from '@/context/NavigationContext'

export interface Word {
  id: number
  quebecois: string
  standard_french: string
  english: string
  pronunciation?: string
  usage_notes?: string
  correct_count: number
  wrong_count: number
  groups?: Array<{ id: number; name: string; }>
}

export default function WordShow() {
  const { wordId } = useParams<{ wordId: string }>()
  const { setCurrentWord } = useNavigation()

  const queryOptions = {
    queryKey: ['word', wordId],
    queryFn: async () => {
      const response = await api.get<{ word: Word }>(`/words/${wordId}`)
      return response.data.word
    },
  } as const

  const { data: word, isLoading, error } = useQuery(queryOptions)

  if (isLoading) {
    return <div className="text-center py-4">Loading...</div>
  }

  if (error || !word) {
    return <div className="text-red-500 text-center py-4">Failed to load word details</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Word Details</h1>
        <Link
          to="/words"
          className="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 dark:text-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600"
        >
          Back to Words
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="p-6 space-y-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Quebecois</h2>
            <p className="mt-1 text-3xl text-gray-600 dark:text-gray-300">{word.quebecois}</p>
          </div>

          <div>
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Standard French</h2>
            <p className="mt-1 text-xl text-gray-600 dark:text-gray-300">{word.standard_french}</p>
          </div>

          <div>
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">English</h2>
            <p className="mt-1 text-xl text-gray-600 dark:text-gray-300">{word.english}</p>
          </div>

          {word.pronunciation && (
            <div>
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Pronunciation</h2>
              <p className="mt-1 text-xl text-gray-600 dark:text-gray-300">{word.pronunciation}</p>
            </div>
          )}

          {word.usage_notes && (
            <div>
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Usage Notes</h2>
              <p className="mt-1 text-xl text-gray-600 dark:text-gray-300">{word.usage_notes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}