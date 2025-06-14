// application.js - Fixed version with validation for interests/contributions and UCE/UACE years
document.addEventListener('DOMContentLoaded', function () {
    let darkMode = false;
    let formData = {};
    
    const modeToggle = document.getElementById('mode-toggle');
    if (modeToggle) {
        modeToggle.addEventListener('click', function () {
            darkMode = !darkMode;
            document.body.classList.toggle('dark-mode', darkMode);

            if (darkMode) {
                this.innerHTML = '<i class="bi bi-sun-fill"></i> Light Mode';
            } else {
                this.innerHTML = '<i class="bi bi-moon-fill"></i> Dark Mode';
            }
        });
    }

    // Form validation and submission
    (function () {
        'use strict'

        const forms = document.querySelectorAll('.needs-validation');
        const form = document.getElementById('alumni-form');

        // Handle UCE/UACE radio buttons and year fields
        const uceYesRadio = document.getElementById('id_sat_uce_yes');
        const uceNoRadio = document.getElementById('id_sat_uce_no');
        const uaceYesRadio = document.getElementById('id_sat_uace_yes');
        const uaceNoRadio = document.getElementById('id_sat_uace_no');
        const uceYearField = document.getElementById('id_uce_class_year');
        const uaceYearField = document.getElementById('id_uace_class_year');

        function handleUCEChange() {
            if (uceYesRadio && uceYesRadio.checked) {
                uceYearField.disabled = false;
                uceYearField.required = true;
            } else {
                uceYearField.disabled = true;
                uceYearField.required = false;
                uceYearField.value = '';
            }
        }

        function handleUACEChange() {
            if (uaceYesRadio && uaceYesRadio.checked) {
                uaceYearField.disabled = false;
                uaceYearField.required = true;
            } else {
                uaceYearField.disabled = true;
                uaceYearField.required = false;
                uaceYearField.value = '';
            }
        }

        // Initialize UCE/UACE handlers
        if (uceYesRadio && uceNoRadio) {
            uceYesRadio.addEventListener('change', handleUCEChange);
            uceNoRadio.addEventListener('change', handleUCEChange);
            handleUCEChange();
        }

        if (uaceYesRadio && uaceNoRadio) {
            uaceYesRadio.addEventListener('change', handleUACEChange);
            uaceNoRadio.addEventListener('change', handleUACEChange);
            handleUACEChange();
        }

        // Form submission validation
        if (form) {
            form.addEventListener('submit', function (event) {
                console.log('Form submission triggered');
                
                let isFormValid = true;
                let errorMessages = [];

                // Validate classes attended checkboxes
                const classesCheckboxes = form.querySelectorAll('input[name="classes_attended"]:checked');
                if (classesCheckboxes.length === 0) {
                    errorMessages.push('Please select at least one class attended.');
                    isFormValid = false;
                }

                // Validate at least one area of interest is selected
                const interestCheckboxes = form.querySelectorAll('#interests input[name^="mentorship"], #interests input[name^="skill"], #interests input[name^="network"], #interests input[name^="fundraisers"], #interests input[name^="event_planning"], #interests input[name^="cohort"], #interests input[name^="volunteering"]:checked');
                if (interestCheckboxes.length === 0) {
                    errorMessages.push('Please select at least one Area of Interest.');
                    isFormValid = false;
                }

                // Validate at least one area of contribution is selected
                const contributionCheckboxes = form.querySelectorAll('#interests input[name^="financial"], #interests input[name^="charitable"], #interests input[name^="alumni_sports"], #interests input[name^="alumni_dinner"], #interests input[name^="events_at_school"], #interests input[name^="all_get_together"]:checked');
                if (contributionCheckboxes.length === 0) {
                    errorMessages.push('Please select at least one Area of Contribution.');
                    isFormValid = false;
                }

                // Validate UCE/UACE years if applicable
                if (uceYesRadio && uceYesRadio.checked && !uceYearField.value) {
                    errorMessages.push('Please enter your UCE Class Year.');
                    isFormValid = false;
                }

                if (uaceYesRadio && uaceYesRadio.checked && !uaceYearField.value) {
                    errorMessages.push('Please enter your UACE Class Year.');
                    isFormValid = false;
                }

                // Validate consent checkbox
                const consentCheckbox = document.getElementById('id_consent_given');
                if (!consentCheckbox || !consentCheckbox.checked) {
                    errorMessages.push('You must agree to the terms and conditions to proceed.');
                    isFormValid = false;
                }

                // Validate all required fields across all tabs
                const allRequiredFields = form.querySelectorAll('[required]');
                let firstInvalidField = null;
                
                allRequiredFields.forEach(field => {
                    if (field.disabled) return;
                    
                    let fieldValid = true;
                    
                    if (field.type === 'checkbox' && field.name === 'classes_attended') {
                        return; // Already validated above
                    } else if (field.type === 'checkbox') {
                        fieldValid = field.checked;
                    } else if (field.type === 'radio') {
                        const radioGroup = form.querySelectorAll(`input[name="${field.name}"]`);
                        fieldValid = Array.from(radioGroup).some(radio => radio.checked);
                    } else {
                        fieldValid = field.value.trim() !== '';
                    }

                    if (!fieldValid) {
                        field.classList.add('is-invalid');
                        if (!firstInvalidField) {
                            firstInvalidField = field;
                        }
                        isFormValid = false;
                    } else {
                        field.classList.remove('is-invalid');
                    }
                });

                // If form is invalid, prevent submission and show errors
                if (!isFormValid) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    form.classList.add('was-validated');
                    
                    // Navigate to the tab with the first error
                    if (firstInvalidField) {
                        const tabPane = firstInvalidField.closest('.tab-pane');
                        if (tabPane) {
                            const tabId = tabPane.id;
                            const tabButton = document.getElementById(tabId + '-tab');
                            if (tabButton) {
                                const tab = new bootstrap.Tab(tabButton);
                                tab.show();
                            }
                        }
                    }
                    
                    // If we have specific error messages, show them
                    if (errorMessages.length > 0) {
                        showErrorMessage(errorMessages.join(' '));
                    } else {
                        showErrorMessage('Please correct the errors and try again.');
                    }
                    return false;
                }

                // If we reach here, form is valid
                console.log('Form is valid, proceeding with submission');
                form.classList.add('was-validated');
                
                // Show loading state on submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
                    
                    // Re-enable button after 10 seconds as fallback
                    setTimeout(() => {
                        if (submitBtn.disabled) {
                            submitBtn.disabled = false;
                            submitBtn.innerHTML = 'Submit Application';
                        }
                    }, 10000);
                }
                
                // Allow form to submit naturally
                return true;
            });
        }

        // Tab navigation
        const tabs = document.querySelectorAll('.nav-link');
        const tabsArray = Array.from(tabs);

        function validateCurrentTab(tabContent) {
            const requiredFields = tabContent.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (field.disabled) return;
                
                let fieldValid = true;
                
                if (field.type === 'checkbox') {
                    if (field.name === 'classes_attended') {
                        const checkedBoxes = tabContent.querySelectorAll('input[name="classes_attended"]:checked');
                        fieldValid = checkedBoxes.length > 0;
                    } else {
                        fieldValid = field.checked;
                    }
                } else if (field.type === 'radio') {
                    const radioGroup = tabContent.querySelectorAll(`input[name="${field.name}"]`);
                    fieldValid = Array.from(radioGroup).some(radio => radio.checked);
                } else {
                    fieldValid = field.value.trim() !== '';
                }

                if (!fieldValid) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            // Special validation for interests tab
            if (tabContent.id === 'interests') {
                // Check at least one interest is selected
                const interestCheckboxes = tabContent.querySelectorAll('input[name^="mentorship"], input[name^="skill"], input[name^="network"], input[name^="fundraisers"], input[name^="event_planning"], input[name^="cohort"], input[name^="volunteering"]:checked');
                if (interestCheckboxes.length === 0) {
                    isValid = false;
                    showErrorMessage('Please select at least one Area of Interest.');
                }

                // Check at least one contribution is selected
                const contributionCheckboxes = tabContent.querySelectorAll('input[name^="financial"], input[name^="charitable"], input[name^="alumni_sports"], input[name^="alumni_dinner"], input[name^="events_at_school"], input[name^="all_get_together"]:checked');
                if (contributionCheckboxes.length === 0) {
                    isValid = false;
                    showErrorMessage('Please select at least one Area of Contribution.');
                }
            }

            return isValid;
        }

        function showErrorMessage(message) {
            // Remove existing alerts
            const existingAlerts = document.querySelectorAll('.alert-danger');
            existingAlerts.forEach(alert => alert.remove());
            
            // Create new alert
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            // Insert at top of form container
            const formContainer = document.querySelector('.form-container');
            formContainer.insertBefore(alertDiv, formContainer.firstChild);
            
            // Auto-remove after 8 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 8000);
        }

        // Next button functionality
        document.querySelectorAll('.next-tab').forEach(button => {
            button.addEventListener('click', () => {
                const activeTab = document.querySelector('.nav-link.active');
                const currentIndex = tabsArray.indexOf(activeTab);
                const currentTabContent = document.querySelector('.tab-pane.active');

                if (currentTabContent && !validateCurrentTab(currentTabContent)) {
                    return;
                }

                // Remove any validation alerts
                const existingAlert = currentTabContent?.querySelector('.alert-danger');
                if (existingAlert) existingAlert.remove();

                if (currentIndex < tabsArray.length - 1) {
                    const nextTab = new bootstrap.Tab(tabsArray[currentIndex + 1]);
                    nextTab.show();
                    updateProgress(currentIndex + 1);
                }
            });
        });

        // Previous button functionality
        document.querySelectorAll('.prev-tab').forEach(button => {
            button.addEventListener('click', () => {
                const activeTab = document.querySelector('.nav-link.active');
                const currentIndex = tabsArray.indexOf(activeTab);

                if (currentIndex > 0) {
                    const prevTab = new bootstrap.Tab(tabsArray[currentIndex - 1]);
                    prevTab.show();
                    updateProgress(currentIndex - 1);
                }
            });
        });

        function updateProgress(index) {
            const progressBar = document.getElementById('progress-bar');
            const progressText = document.getElementById('progress-text');

            if (progressBar && progressText) {
                const progressPercentage = ((index + 1) / tabsArray.length) * 100;
                progressBar.style.width = progressPercentage + '%';
                progressText.textContent = `Step ${index + 1} of ${tabsArray.length}`;
            }
        }

        // Auto-save form data in memory
        if (form) {
            form.addEventListener('input', function (e) {
                const currentFormData = new FormData(form);
                formData = {};

                currentFormData.forEach((value, key) => {
                    if (formData[key]) {
                        if (Array.isArray(formData[key])) {
                            formData[key].push(value);
                        } else {
                            formData[key] = [formData[key], value];
                        }
                    } else {
                        formData[key] = value;
                    }
                });
            });
        }

        // Handle house dropdown default selection
        const houseSelect = document.getElementById('id_house');
        if (houseSelect && !houseSelect.value) {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select House';
            houseSelect.insertBefore(defaultOption, houseSelect.firstChild);
            houseSelect.value = '';
        }
    })();

    // Initialize Bootstrap tooltips
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});