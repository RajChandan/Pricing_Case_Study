import React, { useEffect, useState } from "react";
import API from "../api";

const RecordsList = ({ records, onEdit, refresh }) => {
  const [allRecords, setAllRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ next: null, previous: null });
  const [page, setPage] = useState(1);

  const fetchRecords = async (pageNumber = 1) => {
    setLoading(true);
    try {
      const response = await API.get(`/records/?page=${pageNumber}`);
      setAllRecords(response.data.results || []);
      setPagination({
        next: response.data.next,
        previous: response.data.previous,
      });
    } catch (error) {
      console.error("Error fetching records:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (records && records.length > 0) {
      setAllRecords(records); // Display search results
    } else {
      fetchRecords(page); // Default records
    }
  }, [records, refresh, page]);

  return (
    <div>
      {loading ? (
        <p>Loading records...</p>
      ) : allRecords.length > 0 ? (
        <>
          <table className="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Store ID</th>
                <th>SKU</th>
                <th>Product Name</th>
                <th>Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {allRecords.map((record) => (
                <tr key={record.id}>
                  <td>{record.store_id}</td>
                  <td>{record.sku}</td>
                  <td>{record.name}</td>
                  <td>${record.price}</td>
                  <td>
                    <button
                      className="btn btn-warning btn-sm"
                      onClick={() => onEdit(record)}
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div>
            {pagination.previous && (
              <button onClick={() => setPage(page - 1)}>Previous</button>
            )}
            {pagination.next && (
              <button onClick={() => setPage(page + 1)}>Next</button>
            )}
          </div>
        </>
      ) : (
        <p>No records available.</p>
      )}
    </div>
  );
};

export default RecordsList;
