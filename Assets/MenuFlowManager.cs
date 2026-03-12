using UnityEngine;
using UnityEngine.UI;

public class MenuFlowManager : MonoBehaviour
{
    public GameObject mainMenuCanvas;
    public GameObject userChoiceCanvas;

    public Button confirmButton;
    public Button patientButton;
    public Button surgeonButton;

    private string selectedMode = "";

    // Colours
    public Color normalColor = Color.white;
    public Color selectedColor = Color.green;

    void Start()
    {
        mainMenuCanvas.SetActive(true);
        userChoiceCanvas.SetActive(false);

        confirmButton.interactable = false;

        ResetButtonHighlights();
    }

    public void GoToUserChoice()
    {
        mainMenuCanvas.SetActive(false);
        userChoiceCanvas.SetActive(true);
    }

    public void GoBackToIntro()
    {
        userChoiceCanvas.SetActive(false);
        mainMenuCanvas.SetActive(true);
    }

    public void SelectPatient()
    {
        selectedMode = "Patient";
        confirmButton.interactable = true;

        ResetButtonHighlights();
        patientButton.image.color = selectedColor;
    }

    public void SelectSurgeon()
    {
        selectedMode = "Surgeon";
        confirmButton.interactable = true;

        ResetButtonHighlights();
        surgeonButton.image.color = selectedColor;
    }

    public void ConfirmSelection()
    {
        Debug.Log("Selected Mode: " + selectedMode);

        mainMenuCanvas.SetActive(false);
        userChoiceCanvas.SetActive(false);
    }

    void ResetButtonHighlights()
    {
        patientButton.image.color = normalColor;
        surgeonButton.image.color = normalColor;
    }
}