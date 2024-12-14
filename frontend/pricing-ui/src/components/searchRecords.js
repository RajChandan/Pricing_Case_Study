import React, { useState } from "react";
import API from "../api";

const SearchRecords = ({ onSearchSuccess }) => {
  const [formData, setFormData] = useState({
    store_id: "",
    sku: "",
    name: "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Construct query string for GET request
      const query = new URLSearchParams(formData).toString();
      const response = await API.get(`/search/?${query}`);
      console.log("Search Response:", response.data);
      onSearchSuccess(response.data); // Pass search results to parent
    } catch (error) {
      console.error("Error searching records:", error);
      alert("No records found or search failed.");
      onSearchSuccess([]); // Pass an empty array if search fails
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-3">
      <div className="mb-2">
        <label>Store ID</label>
        <input
          type="text"
          className="form-control"
          name="store_id"
          value={formData.store_id}
          onChange={handleChange}
        />
      </div>
      <div className="mb-2">
        <label>SKU</label>
        <input
          type="text"
          className="form-control"
          name="sku"
          value={formData.sku}
          onChange={handleChange}
        />
      </div>
      <div className="mb-2">
        <label>Product Name</label>
        <input
          type="text"
          className="form-control"
          name="name"
          value={formData.name}
          onChange={handleChange}
        />
      </div>
      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
};

export default SearchRecords;
