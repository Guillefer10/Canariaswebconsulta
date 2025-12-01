import { ReactNode } from 'react'

export const DataTable = ({ headers, rows }: { headers: string[]; rows: ReactNode[] }) => (
  <table className="table">
    <thead>
      <tr>
        {headers.map((h) => (
          <th key={h}>{h}</th>
        ))}
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
)
