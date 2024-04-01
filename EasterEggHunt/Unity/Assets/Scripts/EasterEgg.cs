using PLUME.Core.Recorder;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

[RequireComponent(typeof(XRSimpleInteractable))]
public class EasterEgg : MonoBehaviour
{
    public Quest quest;

    private XRSimpleInteractable _interactable;

    private void Start()
    {
        _interactable = GetComponent<XRSimpleInteractable>();
        _interactable.hoverEntered.AddListener(ObjectPickedUp);
    }

    private void ObjectPickedUp(HoverEnterEventArgs args)
    {
        if (PlumeRecorder.IsRecording)
        {
            PlumeRecorder.RecordMarker("Egg Pick Up");
        }

        quest.OnEggPickUp(this);
    }
}