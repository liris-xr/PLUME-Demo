using PLUME.Core.Recorder;
using UnityEngine;

public class RoomFlowEventMarker : MonoBehaviour
{
    public Collider playerCollider;

    private void OnTriggerEnter(Collider other)
    {
        if (other == playerCollider)
        {
            if (PlumeRecorder.IsRecording)
            {
                PlumeRecorder.RecordMarker("Enter Room : " + gameObject.name);
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other == playerCollider)
        {
            if (PlumeRecorder.IsRecording)
            {
                PlumeRecorder.RecordMarker("Exit Room : " + gameObject.name);
            }
        }
    }
}