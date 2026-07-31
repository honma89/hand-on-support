"use client";

import { useState } from "react";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useUsers, useUpdateUser } from "@/lib/hooks/use-users";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import type { User, UserRole } from "@/lib/types";

const ROLE_OPTIONS: UserRole[] = ["volunteer", "organizer", "admin"];

function UserRow({ user, isSelf }: { user: User; isSelf: boolean }) {
  const updateUser = useUpdateUser();
  const [pendingRole, setPendingRole] = useState<UserRole | null>(null);

  const handleRoleChange = (newRole: UserRole) => {
    if (newRole === user.role) return;
    if (isSelf) {
      window.alert("You can't change your own role from here.");
      return;
    }
    if (
      user.role === "admin" &&
      !window.confirm(`Demote ${user.full_name} from admin to ${newRole}?`)
    ) {
      return;
    }
    setPendingRole(newRole);
    updateUser.mutate(
      { userId: user.id, data: { role: newRole } },
      { onSettled: () => setPendingRole(null) },
    );
  };

  const handleToggleActive = () => {
    if (isSelf) {
      window.alert("You can't deactivate your own account from here.");
      return;
    }
    if (
      user.is_active &&
      !window.confirm(`Deactivate ${user.full_name}? They won't be able to log in.`)
    ) {
      return;
    }
    updateUser.mutate({ userId: user.id, data: { is_active: !user.is_active } });
  };

  return (
    <tr className="border-b border-outline/20 last:border-0">
      <td className="py-sm pr-md">
        <p className="font-label-md text-label-md text-on-surface">{user.full_name}</p>
        <p className="font-body-md text-sm text-on-surface-variant">{user.email}</p>
      </td>
      <td className="py-sm pr-md">
        <Select
          value={pendingRole ?? user.role}
          disabled={isSelf || updateUser.isPending}
          onChange={(e) => handleRoleChange(e.target.value as UserRole)}
          className="w-40"
        >
          {ROLE_OPTIONS.map((role) => (
            <option key={role} value={role}>
              {role.charAt(0).toUpperCase() + role.slice(1)}
            </option>
          ))}
        </Select>
      </td>
      <td className="py-sm pr-md">
        <span
          className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${
            user.is_active
              ? "bg-primary-container text-on-primary-container"
              : "bg-error/10 text-error"
          }`}
        >
          {user.is_active ? "Active" : "Inactive"}
        </span>
      </td>
      <td className="py-sm text-right">
        <Button
          variant={user.is_active ? "outline" : "secondary"}
          size="sm"
          disabled={isSelf || updateUser.isPending}
          onClick={handleToggleActive}
        >
          {user.is_active ? "Deactivate" : "Activate"}
        </Button>
      </td>
    </tr>
  );
}

export default function ManageUsersPage() {
  const { data: currentUser } = useCurrentUser();
  const { data: users, isLoading, isError } = useUsers();

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-5xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs">
          Manage Users
        </h1>
        <p className="font-body-md text-body-md text-on-surface-variant mb-lg">
          Change a volunteer&apos;s role or deactivate their account.
        </p>

        {isLoading && (
          <p className="text-on-surface-variant font-body-md text-body-md">Loading users…</p>
        )}
        {isError && (
          <p className="text-error font-body-md text-body-md">
            Could not load users. Admin access is required.
          </p>
        )}

        {users && (
          <div className="glass-card rounded-xl p-md shadow-ambient overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-outline/30">
                  <th className="pb-sm font-label-md text-label-md text-on-surface-variant">
                    User
                  </th>
                  <th className="pb-sm font-label-md text-label-md text-on-surface-variant">
                    Role
                  </th>
                  <th className="pb-sm font-label-md text-label-md text-on-surface-variant">
                    Status
                  </th>
                  <th className="pb-sm"></th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <UserRow key={user.id} user={user} isSelf={user.id === currentUser?.id} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}
