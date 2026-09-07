function StatCard({ title, value, description }) {
  return (
    <div className="stat-card">
      <h3>{title}</h3>

      <div className="stat-value">
        {value}
      </div>

      {description && (
        <p>{description}</p>
      )}
    </div>
  );
}

export default StatCard;