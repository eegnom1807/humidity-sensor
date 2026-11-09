import { NavLink, Outlet } from "react-router-dom"
import { LayoutDashboard, Leaf, Cpu } from "lucide-react"
import { cn } from "@/lib/utils"
import { Toaster } from 'sonner';

const navItems = [
  { to: "/", label: "Panel", icon: LayoutDashboard },
  { to: "/plants", label: "Plantas", icon: Leaf },
  { to: "/sensors", label: "Sensores", icon: Cpu },
]

export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <Leaf className="h-6 w-6 text-green-600" />
            <span className="hidden sm:inline text-xl font-bold">Monitor de plantas</span>
          </div>
          <nav className="flex items-center gap-1">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
                    isActive
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground"
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <Toaster richColors position="top-right" expand={true} />
        <Outlet />
      </main>
    </div>
  )
}
