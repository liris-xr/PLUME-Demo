using PLUME.Core.Recorder;
using UnityEngine;

public class PlumeAutoStart : MonoBehaviour
{
    public void Start()
    {
        PlumeRecorder.StartRecording("EggHunt");
    }
}