import { useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useWordDetails } from '../hooks/useWordDetails'
import { useNavigation } from '../context/NavigationContext'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Skeleton } from '../components/ui/skeleton'

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
  const { id } = useParams<{ id: string }>()
  const { data: word, isLoading, error } = useWordDetails(id!)
  const { setCurrentWord } = useNavigation()

  useEffect(() => {
    if (word) {
      setCurrentWord(word)
    }
    return () => setCurrentWord(null)
  }, [word, setCurrentWord])

  if (isLoading) {
    return (
      <div className="space-y-6" data-testid="loading-skeleton">
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-48" />
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Skeleton className="h-4 w-24 mb-2" />
                <Skeleton className="h-6 w-32" />
              </div>
              <div>
                <Skeleton className="h-4 w-24 mb-2" />
                <Skeleton className="h-6 w-32" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <Card className="border-destructive">
        <CardContent className="pt-6">
          <p className="text-destructive">Error: {error.message}</p>
        </CardContent>
      </Card>
    )
  }

  if (!word) {
    return (
      <Card className="border-destructive">
        <CardContent className="pt-6">
          <p className="text-destructive">Word not found</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{word.quebecois}</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-sm font-medium text-muted-foreground">Standard French</dt>
              <dd className="text-lg">{word.standard_french}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-muted-foreground">English</dt>
              <dd className="text-lg">{word.english}</dd>
            </div>
            {word.pronunciation && (
              <div>
                <dt className="text-sm font-medium text-muted-foreground">Pronunciation</dt>
                <dd className="text-lg">{word.pronunciation}</dd>
              </div>
            )}
            {word.usage_notes && (
              <div className="col-span-2">
                <dt className="text-sm font-medium text-muted-foreground">Usage Notes</dt>
                <dd className="text-lg">{word.usage_notes}</dd>
              </div>
            )}
          </dl>
        </CardContent>
      </Card>

      {word.groups && word.groups.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Groups</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2 flex-wrap">
              {word.groups.map(group => (
                <span 
                  key={group.id}
                  className="px-2 py-1 bg-primary/10 rounded-md text-sm"
                >
                  {group.name}
                </span>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}