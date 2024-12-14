import React, { useState } from "react";
import API from "../api";

const EditRecord = ({ record, onClose, onUpdate }) => {
  const [formData, setFormData] = useState(record);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await API.put(`/records/${formData.id}/`, formData);
      alert("Record updated successfully!");
      onUpdate();
      onClose();
    } catch (error) {
      console.error("Error updating record:", error);
      alert("Failed to update record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label>Store ID</label>
        <input
          className="form-control"
          name="store_id"
          value={formData.store_id}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label>SKU</label>
        <input
          className="form-control"
          name="sku"
          value={formData.sku}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label>Product Name</label>
        <input
          className="form-control"
          name="name"
          value={formData.name}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label>Price</label>
        <input
          className="form-control"
          name="price"
          value={formData.price}
          onChange={handleChange}
        />
      </div>
      <button type="submit" className="btn btn-success me-2" disabled={loading}>
        {loading ? "Saving..." : "Save"}
      </button>
      <button type="button" className="btn btn-secondary" onClick={onClose}>
        Cancel
      </button>
    </form>
  );
};

export default EditRecord;
