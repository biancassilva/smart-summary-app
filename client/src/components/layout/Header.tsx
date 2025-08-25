interface HeaderProps {
  title?: string;
}

export function Header({ title = "Smart Summary App" }: HeaderProps) {
  return (
    <div className="text-center mb-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">{title}</h1>
    </div>
  );
}
