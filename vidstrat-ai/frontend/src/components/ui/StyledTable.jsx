import { scoreColor } from './helpers'

export default function StyledTable({ columns, rows, scoreKeys = [], winner }) {
  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full min-w-[760px] border-collapse bg-card text-left text-sm">
        <thead className="bg-primary text-white">
          <tr>
            {columns.map((column) => <th key={column.key} className="px-4 py-3 font-bold">{column.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.company || row.name || index}`} className={`${index % 2 ? 'bg-card' : 'bg-surface/45'} ${winner && (row.company === winner || row.name === winner) ? 'bg-primary/10' : ''} transition-colors hover:bg-white/5`}>
              {columns.map((column) => (
                <td key={column.key} className={`px-4 py-3 ${scoreKeys.includes(column.key) ? scoreColor(row[column.key]) : 'text-muted'}`}>
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
