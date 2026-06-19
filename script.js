// Sample user data
let users = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'admin', status: 'active' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'user', status: 'active' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'viewer', status: 'inactive' },
    { id: 4, name: 'Alice Brown', email: 'alice@example.com', role: 'user', status: 'suspended' },
    { id: 5, name: 'Charlie Wilson', email: 'charlie@example.com', role: 'user', status: 'active' },
];

// DOM Elements
const usersTable = document.getElementById('usersTable');
const userForm = document.getElementById('userForm');
const userModal = document.getElementById('userModal');
const confirmModal = document.getElementById('confirmModal');
const addUserBtn = document.getElementById('addUserBtn');
const modalTitle = document.getElementById('modalTitle');
const userIdInput = document.getElementById('userId');
const passwordFields = document.querySelectorAll('.password-fields');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const pageInfo = document.getElementById('pageInfo');
const searchInput = document.querySelector('.search-box input');

// Pagination variables
let currentPage = 1;
const usersPerPage = 5;
let filteredUsers = [...users];

// Initialize the app
function init() {
    renderUsersTable();
    setupEventListeners();
}

// Render users table
function renderUsersTable() {
    const tbody = usersTable.querySelector('tbody');
    tbody.innerHTML = '';

    const startIndex = (currentPage - 1) * usersPerPage;
    const endIndex = startIndex + usersPerPage;
    const paginatedUsers = filteredUsers.slice(startIndex, endIndex);

    if (paginatedUsers.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td colspan="6" style="text-align: center;">No users found</td>`;
        tbody.appendChild(tr);
        return;
    }

    paginatedUsers.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
            <td><span class="status ${user.status}">${user.status}</span></td>
            <td class="actions">
                <button class="btn btn-sm btn-secondary edit-btn" data-id="${user.id}">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger delete-btn" data-id="${user.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    // Update pagination info
    const totalPages = Math.ceil(filteredUsers.length / usersPerPage);
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
}

// Setup event listeners
function setupEventListeners() {
    // Add user button
    addUserBtn.addEventListener('click', () => {
        openUserModal('add');
    });

    // Edit and delete buttons (delegated)
    usersTable.addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-btn') || e.target.closest('.edit-btn')) {
            const btn = e.target.classList.contains('edit-btn') ? e.target : e.target.closest('.edit-btn');
            const id = parseInt(btn.getAttribute('data-id'));
            openUserModal('edit', id);
        }

        if (e.target.classList.contains('delete-btn') || e.target.closest('.delete-btn')) {
            const btn = e.target.classList.contains('delete-btn') ? e.target : e.target.closest('.delete-btn');
            const id = parseInt(btn.getAttribute('data-id'));
            confirmDeleteUser(id);
        }
    });

    // Modal close buttons
    document.querySelectorAll('.close').forEach(btn => {
        btn.addEventListener('click', () => {
            userModal.classList.remove('show');
            confirmModal.classList.remove('show');
        });
    });

    // Cancel buttons
    document.getElementById('cancelBtn').addEventListener('click', () => {
        userModal.classList.remove('show');
    });

    document.getElementById('confirmCancel').addEventListener('click', () => {
        confirmModal.classList.remove('show');
    });

    // Form submission
    userForm.addEventListener('submit', handleFormSubmit);

    // Pagination buttons
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderUsersTable();
        }
    });

    nextPageBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(filteredUsers.length / usersPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderUsersTable();
        }
    });

    // Search input
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();
        filteredUsers = users.filter(user => 
            user.name.toLowerCase().includes(searchTerm) || 
            user.email.toLowerCase().includes(searchTerm) ||
            user.role.toLowerCase().includes(searchTerm) ||
            user.status.toLowerCase().includes(searchTerm)
        );
        currentPage = 1;
        renderUsersTable();
    });

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === userModal) {
            userModal.classList.remove('show');
        }
        if (e.target === confirmModal) {
            confirmModal.classList.remove('show');
        }
    });
}

// Open user modal for add/edit
function openUserModal(action, id = null) {
    if (action === 'add') {
        modalTitle.textContent = 'Add New User';
        userIdInput.value = '';
        userForm.reset();
        passwordFields.forEach(field => field.classList.add('show'));
    } else {
        modalTitle.textContent = 'Edit User';
        const user = users.find(u => u.id === id);
        if (user) {
            userIdInput.value = user.id;
            document.getElementById('name').value = user.name;
            document.getElementById('email').value = user.email;
            document.getElementById('role').value = user.role;
            document.getElementById('status').value = user.status;
            passwordFields.forEach(field => field.classList.remove('show'));
        }
    }
    userModal.classList.add('show');
}

// Handle form submission
function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = userIdInput.value ? parseInt(userIdInput.value) : null;
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
    const status = document.getElementById('status').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Simple validation
    if (!name || !email || !role || !status) {
        alert('Please fill in all required fields');
        return;
    }

    if (!id && (!password || !confirmPassword)) {
        alert('Please enter and confirm password for new user');
        return;
    }

    if (password && password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    if (id) {
        // Update existing user
        const index = users.findIndex(u => u.id === id);
        if (index !== -1) {
            users[index] = { ...users[index], name, email, role, status };
        }
    } else {
        // Add new user
        const newId = users.length > 0 ? Math.max(...users.map(u => u.id)) + 1 : 1;
        users.push({ id: newId, name, email, role, status });
    }

    renderUsersTable();
    userModal.classList.remove('show');
}

// Confirm user deletion
function confirmDeleteUser(id) {
    const user = users.find(u => u.id === id);
    if (!user) return;

    document.getElementById('confirmMessage').textContent = `Are you sure you want to delete user ${user.name}?`;
    document.getElementById('confirmAction').textContent = 'Delete';
    document.getElementById('confirmAction').onclick = () => {
        deleteUser(id);
        confirmModal.classList.remove('show');
    };
    confirmModal.classList.add('show');
}

// Delete user
function deleteUser(id) {
    users = users.filter(user => user.id !== id);
    // Reset pagination if needed
    if (filteredUsers.length <= (currentPage - 1) * usersPerPage) {
        currentPage = Math.max(1, currentPage - 1);
    }
    renderUsersTable();
}

// Initialize the app
document.addEventListener('DOMContentLoaded', init);