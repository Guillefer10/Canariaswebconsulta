type ToastProps = {
  type?: 'info' | 'success' | 'warning' | 'error'
  message: string
}

export const Toast = ({ type = 'info', message }: ToastProps) => {
  return <div className={`toast ${type}`}>{message}</div>
}
