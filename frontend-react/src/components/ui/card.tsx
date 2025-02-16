import { forwardRef, type ReactElement } from "react"
import { cn } from "@/lib/utils"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
  children: React.ReactNode
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, children, ...props }): ReactElement => (
    <div
      className={cn(
        "rounded-lg border bg-card text-card-foreground shadow-sm",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
)
Card.displayName = "Card"

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
  children: React.ReactNode
}

const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>((props, ref): JSX.Element => {
  const { className, children, ...rest } = props
  return (
    <div
      ref={ref}
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...rest}
    >
      {children}
    </div>
  )
})
CardHeader.displayName = "CardHeader"

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  className?: string
  children: React.ReactNode
}

const CardTitle = forwardRef<HTMLHeadingElement, CardTitleProps>((props, ref): JSX.Element => {
  const { className, children, ...rest } = props
  return (
    <h3
      ref={ref}
      className={cn(
        "text-2xl font-semibold leading-none tracking-tight",
        className
      )}
      {...rest}
    >
      {children}
    </h3>
  )
})
CardTitle.displayName = "CardTitle"

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
  children: React.ReactNode
}

const CardContent = forwardRef<HTMLDivElement, CardContentProps>((props, ref): JSX.Element => {
  const { className, children, ...rest } = props
  return (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...rest}>
      {children}
    </div>
  )
})
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardContent } 