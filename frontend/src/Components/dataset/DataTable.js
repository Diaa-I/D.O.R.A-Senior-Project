import Data from './data.json';
import { useMemo } from 'react';
import { useTable } from 'react-table';
import './Table.css';
import React from 'react';

function DataTable() {
  const data = useMemo(() => Data, []);
  const columns = useMemo(
    () => [
      {
        Header: 'Dataset Name',
        accessor: 'Dataset Name', 
      },
      {
        Header: 'Size',
        accessor: 'Size', 
      },
      {
        Header: 'Type',
        accessor: 'Type', 
      },
      {
        Header: 'Number of Entries',
        accessor: 'Number of Entries', 
      },
      {
        Header: 'Status',
        accessor: 'Status', 
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data });

  return (
    <div>
      <table {...getTableProps()} className="custom-table">
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()} className="custom-table-row">
              {headerGroup.headers.map((column) => ( // Changed `columns` to `column`
                <th {...column.getHeaderProps()}>
                  {column.render('Header')}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
