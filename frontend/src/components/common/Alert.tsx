type AlertProps = {
  type?: 'info' | 'success' | 'warning' | 'error'
  message: string
}

const Alert = ({ type = 'info', message }: AlertProps) => (
  <div className={`alert ${type}`}>
    {message}
  </div>
)

export default Alert
