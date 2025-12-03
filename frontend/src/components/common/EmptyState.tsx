import { ReactNode } from 'react'

type EmptyStateProps = {
  title: string
  description?: string
  action?: ReactNode
}

const EmptyState = ({ title, description, action }: EmptyStateProps) => (
  <div className="empty-state">
    <div>
      <p className="empty-title">{title}</p>
      {description && <p className="muted">{description}</p>}
    </div>
    {action && <div className="empty-action">{action}</div>}
  </div>
)

export default EmptyState
