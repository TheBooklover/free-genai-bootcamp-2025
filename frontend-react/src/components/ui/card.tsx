import * as React from "react"
import { cn } from "@/lib/utils"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

const Card = ({ className, children, ...props }: CardProps) => (
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
Card.displayName = "Card"

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

const CardHeader = ({ className, children, ...props }: CardHeaderProps) => (
  <div
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  >
    {children}
  </div>
)
CardHeader.displayName = "CardHeader"

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}

const CardTitle = ({ className, children, ...props }: CardTitleProps) => (
  <h3
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  >
    {children}
  </h3>
)
CardTitle.displayName = "CardTitle"

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

const CardContent = ({ className, children, ...props }: CardContentProps) => (
  <div className={cn("p-6 pt-0", className)} {...props}>
    {children}
  </div>
)
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardContent } 