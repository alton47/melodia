interface SidebarProps {
  children: React.ReactNode;
}

const Sidebar: React.FC<SidebarProps> = ({ children }) => {
  return <div>{children}kengee</div>;
};

export default Sidebar;
