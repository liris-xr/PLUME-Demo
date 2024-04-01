using System.Collections;
using Unity.XR.CoreUtils;
using UnityEditor;
using UnityEngine;

public class PlayerManager : MonoBehaviour
{
    public Transform lobbyCameraPosition;
    public XROrigin xrOrigin;

    public void MovePlayerToLobby(bool fade)
    {
        StartCoroutine(MovePlayerToLobbyCoroutine(fade));
    }

    private IEnumerator MovePlayerToLobbyCoroutine(bool fade)
    {
        if (fade)
        {
            OVRScreenFade.instance.fadeTime = 2.0f;
            OVRScreenFade.instance.FadeOut();

            yield return new WaitForSeconds(2);
        }

        var rotationDifference = lobbyCameraPosition.rotation * Quaternion.Inverse(xrOrigin.Camera.transform.rotation);
        var eulerDifference = rotationDifference.eulerAngles;

        xrOrigin.MoveCameraToWorldLocation(lobbyCameraPosition.position);
        xrOrigin.RotateAroundCameraUsingOriginUp(eulerDifference.y);

        if (fade)
        {
            OVRScreenFade.instance.fadeTime = 2.0f;
            OVRScreenFade.instance.FadeIn();
        }
    }

    public void StopApplication()
    {
        StartCoroutine(StopApplicationCoroutine());
    }

    private static IEnumerator StopApplicationCoroutine()
    {
        yield return new WaitForSeconds(10.0f);

        OVRScreenFade.instance.fadeTime = 2.0f;
        OVRScreenFade.instance.FadeOut();

        yield return new WaitForSeconds(2.0f);

        // Check current platform
        if (Application.platform == RuntimePlatform.Android)
        {
            // Call the method to stop the application
            var activity =
                new AndroidJavaClass("com.unity3d.xrOrigin.UnityPlayer")
                    .GetStatic<AndroidJavaObject>("currentActivity");
            activity.Call<bool>("moveTaskToBack", true);
        }
        else
        {
#if UNITY_EDITOR
            // Application.Quit() does not work in the editor so
            // UnityEditor.EditorApplication.isPlaying need to be set to false to endXrOriginPosition the game
            EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
        }
    }
}