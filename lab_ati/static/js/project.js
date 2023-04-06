/* Project specific Javascript goes here. */
class SocialMediaController {
  constructor(idForm) {
    this.idForm = idForm || "form";
    this.socialContainer = document.getElementById(this.idForm);
    this.totalFormsEl = document.getElementById(`id_${this.idForm}-TOTAL_FORMS`);
    this.totalForms = parseInt(this.totalFormsEl.value);
    this.templateRow = this.socialContainer.querySelector(".row:last-child"); // Last Row
    // Setup event listeners for all rows
    this.socialContainer
      .querySelectorAll(".row")
      .forEach((row) => this.setupEvents(row));
    this.editing = this.socialContainer.dataset.editing;

    this.toDeleteArea = this.socialContainer.querySelector("#to-delete");
    this.templateRow.dataset.isEmpty = true;
  }

  // Add delete and add event listners to a row
  setupEvents(element) {
    // Bind methods as events, pass this class instance
    element.addEventListener("click", this.deleteSocialMediaInputs.bind(this));
    element.addEventListener("click", this.addSocialMediaInputs.bind(this));
  }

  // Setup a ROW state
  setupState(element) {
    const inputs = element.querySelectorAll("input");

    inputs.forEach((input) => {
      input.value = "";
    });
  }

  addSocialMediaInputs(event) {
    // This event is activated by event bubbling
    if (event.target.dataset.btnType !== "socialNetworkAddButton") return;

    // Clone the form
    let newRow = this.templateRow.cloneNode(true);

    //Regex to find all instances of the form number
    let formRegex = RegExp(`${this.idForm}-(\\d){1}-`, "g");

    newRow.innerHTML = newRow.innerHTML.replace(
      formRegex,
      `${this.idForm}-${this.totalForms}-`
    ); //Update the new form to have the correct form number

    this.setupEvents(newRow);
    this.setupState(newRow);

    //Insert the new form below the row
    event.currentTarget.insertAdjacentElement("afterend", newRow);

    // Increment formset form count
    this.totalForms += 1;
    this.totalFormsEl.setAttribute("value", this.totalForms);
  }

  deleteSocialMediaInputs(event) {
    // This event is activated by event bubbling
    if (event.target.dataset.btnType !== "socialNetworkRemoveButton") return;

    // Decrease
    if (event.currentTarget.dataset.isEmpty) {
      this.totalForms -= 1;
      this.totalFormsEl.setAttribute("value", this.totalForms);
    }
    if (this.editing) {
      const checkbox = event.currentTarget.querySelector(
        "input[type='checkbox'"
      );

      checkbox.checked = true;

      this.toDeleteArea.appendChild(event.currentTarget);
    }

    if (!this.editing) {
      // Remove
      event.currentTarget.remove();
    }
  }
}
