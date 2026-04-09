"use client";
import { useEffect, useState } from "react";
import "../../styles/table.css";

export default function Students() {
  const [students, setStudents] = useState([]);
  const [name, setName] = useState("");
  const [marks, setMarks] = useState(["", "", "", "", ""]);
  const [editId, setEditId] = useState(null);

  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  // Fetch students
  const fetchStudents = async () => {
    const res = await fetch("http://127.0.0.1:8000/students", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await res.json();
    setStudents(data);
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  // Handle marks change
  const handleMarksChange = (index, value) => {
    const updated = [...marks];
    updated[index] = value;
    setMarks(updated);
  };

  // Add or Update student
  const handleSubmit = async () => {
    const marksFloat = marks.map(Number);

    const url = editId
      ? `http://127.0.0.1:8000/students/id/${editId}`
      : "http://127.0.0.1:8000/students";

    const method = editId ? "PUT" : "POST";

    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name,
        marks: marksFloat,
      }),
    });

    if (res.ok) {
      resetForm();
      fetchStudents();
    } else {
      alert("Error saving student");
    }
  };

  // Edit student
  const handleEdit = (student) => {
    setName(student.name);
    setMarks(
      Array.isArray(student.marks)
        ? student.marks
        : student.marks.split(",")
    );
    setEditId(student.id);
  };

  // Delete student
  const handleDelete = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/students/id/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.ok) {
      fetchStudents();
    } else {
      alert("Delete failed");
    }
  };

  // Reset form
  const resetForm = () => {
    setName("");
    setMarks(["", "", "", "", ""]);
    setEditId(null);
  };

  return (
    <div className="table-container">
      <h2>Student Management</h2>

      {/* Form */}
      <div style={{ marginBottom: "20px" }}>
        <input
          placeholder="Student Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <div>
          {marks.map((m, i) => (
            <input
              key={i}
              placeholder={`Mark ${i + 1}`}
              value={m}
              onChange={(e) => handleMarksChange(i, e.target.value)}
              style={{ width: "60px", margin: "5px" }}
            />
          ))}
        </div>

        <button onClick={handleSubmit}>
          {editId ? "Update Student" : "Add Student"}
        </button>

        {editId && (
          <button onClick={resetForm} style={{ background: "gray" }}>
            Cancel
          </button>
        )}
      </div>

      {/* Table */}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Marks</th>
            <th>Total</th>
            <th>Average</th>
            <th>Grade</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {students.map((s) => (
            <tr key={s.id}>
              <td>{s.id}</td>
              <td>{s.name}</td>
              <td>
                {Array.isArray(s.marks)
                  ? s.marks.join(", ")
                  : s.marks}
              </td>
              <td>{s.totalmarks}</td>
              <td>{s.average}</td>
              <td>{s.grade}</td>
              <td>
                <button onClick={() => handleEdit(s)}>Edit</button>
                <button onClick={() => handleDelete(s.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}