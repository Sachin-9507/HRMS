function Input({
  label,
  type = "text",
  value,
  onChange,
  placeholder = "",
  name,
  required = false,
}) {
  return (
    <div className="form-group">
      {label && <label htmlFor={name}>{label}</label>}

      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="form-input"
      />
    </div>
  );
}

export default Input;