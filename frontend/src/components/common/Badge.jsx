function Badge({ status }) {
  const normalizedStatus = String(status || "")
    .toLowerCase()
    .replaceAll("_", "-");

  return (
    <span className={`badge badge-${normalizedStatus}`}>
      {status || "N/A"}
    </span>
  );
}

export default Badge;