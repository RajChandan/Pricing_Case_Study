import React, { useState } from "react";
import UploadCSV from "../components/uploadCSV";
import SearchRecords from "../components/searchRecords";
import RecordsList from "../components/recordsList";
import EditRecord from "../components/editRecord";

const Home = () => {
  const [searchResults, setSearchResults] = useState([]); // Search results
  const [refreshData, setRefreshData] = useState(false); // Trigger refresh
  const [editingRecord, setEditingRecord] = useState(null);

  const handleSearchSuccess = (results) => {
    console.log("Received Search Results:", results);
    setSearchResults(results); // Update the records list
  };

  const handleFileUpload = () => {
    alert("File uploaded successfully!");
    setRefreshData(!refreshData); // Refresh table
    setSearchResults([]); // Reset search results
  };

  const handleEdit = (record) => {
    setEditingRecord(record);
  };

  const handleUpdate = () => {
    setRefreshData(!refreshData);
    setEditingRecord(null);
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Pricing Management Dashboard</h1>
      <div className="row">
        <div className="col-md-4">
          <UploadCSV onFileUpload={handleFileUpload} />
          <SearchRecords onSearchSuccess={handleSearchSuccess} />
        </div>
        <div className="col-md-8">
          <RecordsList
            records={searchResults} // Pass search results
            onEdit={handleEdit}
            refresh={refreshData}
          />
          {editingRecord && (
            <div className="mt-4">
              <h5>Edit Record</h5>
              <EditRecord
                record={editingRecord}
                onClose={() => setEditingRecord(null)}
                onUpdate={handleUpdate}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
